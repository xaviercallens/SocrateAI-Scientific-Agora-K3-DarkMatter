#!/usr/bin/env python3
"""
Agora@Home: Chameleon Dark Sector Fringe Tracker
Developed by Xavier Callens & Agora Swarm Architecture
License: Strong Copyleft (GPL v3)

This script uses OpenCV to capture the video feed of a Michelson Interferometer's
concentric laser interference rings (fringe pattern). It extracts a 1D cross-section,
applies Gaussian smoothing, and tracks the sub-pixel movement of the fringe peaks.
It bins the tracked shifts into 1-hour blocks to filter out high-frequency seismic noise,
logs the telemetry locally, and periodically streams the daily phase vector to the
central FastAPI server in Cagnes-sur-Mer.
"""

import os
import sys
import time
import argparse
import logging
import csv
import json
import numpy as np
import cv2

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("ChameleonTracker")

class FringeTracker:
    def __init__(self, device=0, resolution=(640, 480), headless=False, upload=False, server_url=None):
        self.device = device
        self.resolution = resolution
        self.headless = headless
        self.upload = upload
        self.server_url = server_url or "http://cagnes-sur-mer.socrateai.net/api/upload_fringe_data"
        
        # Telemetry storage
        self.telemetry_file = "fringe_telemetry.csv"
        self.init_csv()
        
        # Tracking states
        self.roi = None
        self.baseline_peaks = None
        self.hourly_shifts = []
        self.last_hour_timestamp = time.time()
        self.last_upload_timestamp = time.time()
        
        # Initialize video capture
        logger.info(f"Opening camera device {self.device} at resolution {self.resolution}...")
        self.cap = cv2.VideoCapture(self.device)
        if not self.cap.isOpened():
            logger.error(f"Could not open camera device {self.device}.")
            sys.exit(1)
            
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        
    def init_csv(self):
        """Initialize the local telemetry CSV file."""
        if not os.path.exists(self.telemetry_file):
            with open(self.telemetry_file, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Datetime", "Mean_Phase_Shift_Pixels", "Variance", "Samples_Count"])
            logger.info(f"Created local telemetry file: {self.telemetry_file}")

    def select_roi(self, frame):
        """Prompt user to select Region of Interest containing the interference rings."""
        if self.headless:
            # Fallback default ROI in the center of the frame
            h, w = frame.shape[:2]
            self.roi = (w // 4, h // 4, w // 2, h // 2)
            logger.info(f"Headless mode active. Using default central ROI: {self.roi}")
            return
            
        logger.info("==================================================")
        logger.info("SELECT REGION OF INTEREST (ROI) WINDOW")
        logger.info("1. Click and drag a bounding box over the concentric ring pattern.")
        logger.info("2. Press ENTER or SPACE to confirm.")
        logger.info("3. Press 'c' to cancel and use the full frame.")
        logger.info("==================================================")
        
        # Use OpenCV's built-in ROI selector
        roi = cv2.selectROI("Agora@Home - Select Laser Ring Region", frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow("Agora@Home - Select Laser Ring Region")
        
        if roi and roi[2] > 10 and roi[3] > 10:
            self.roi = roi
            logger.info(f"Selected custom ROI: {self.roi}")
        else:
            self.roi = (0, 0, frame.shape[1], frame.shape[2])
            logger.warn("No valid ROI selected. Tracking entire frame.")

    def find_subpixel_peaks(self, profile):
        """
        Locates the coordinates of intensity peaks with sub-pixel precision.
        Applies a local quadratic interpolation:
        p_sub = p + 0.5 * (y_left - y_right) / (y_left - 2 * y_center + y_right)
        """
        peaks = []
        # Basic peak-finding on a 1D smoothed array (local maxima check)
        for i in range(1, len(profile) - 1):
            if profile[i] > profile[i - 1] and profile[i] > profile[i + 1]:
                # Threshold to ignore background noise
                if profile[i] > 20: 
                    # Quadratic interpolation for sub-pixel accuracy
                    y_left = float(profile[i - 1])
                    y_center = float(profile[i])
                    y_right = float(profile[i + 1])
                    
                    denom = (y_left - 2.0 * y_center + y_right)
                    if denom != 0:
                        shift = 0.5 * (y_left - y_right) / denom
                        sub_pixel_pos = i + shift
                        peaks.append(sub_pixel_pos)
        return peaks

    def log_hourly_data(self):
        """Averages the binned fringe movements and logs them to the CSV file."""
        if not self.hourly_shifts:
            return
            
        mean_shift = float(np.mean(self.hourly_shifts))
        variance = float(np.var(self.hourly_shifts))
        count = len(self.hourly_shifts)
        current_time = time.time()
        datetime_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
        
        with open(self.telemetry_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([current_time, datetime_str, mean_shift, variance, count])
            
        logger.info(f"LOGGED HOURLY BLOCK: Shift = {mean_shift:.4f} px | Var = {variance:.6f} | Samples = {count}")
        
        # Clear hourly accumulator and reset timestamp
        self.hourly_shifts = []
        self.last_hour_timestamp = current_time

    def trigger_upload(self):
        """Simulates or executes physical cloud upload of binned data to Cagnes-sur-Mer."""
        logger.info("Initializing daily federated upload to FastAPI server...")
        
        # Gather recent logs
        if not os.path.exists(self.telemetry_file):
            return
            
        payload = []
        with open(self.telemetry_file, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                payload.append(row)
                
        # Only upload the last 24 hours of logs
        payload_subset = payload[-24:]
        
        logger.info(f"Payload compiled: {len(payload_subset)} hourly vectors. Target: {self.server_url}")
        
        # Attempt standard HTTP POST upload
        try:
            import urllib.request
            req = urllib.request.Request(self.server_url, method="POST")
            req.add_header('Content-Type', 'application/json')
            
            data = json.dumps({"telemetry": payload_subset, "client_id": "People_Interferometer_06"}).encode('utf-8')
            
            # Since this is a distributed user script, we set a brief timeout
            with urllib.request.urlopen(req, data=data, timeout=5) as response:
                res_body = response.read().decode('utf-8')
                logger.info(f"UPLOAD SUCCESS: Server Response: {res_body}")
        except Exception as e:
            logger.warn(f"Cloud upload failed (expected if offline or during dry-run): {e}")
            logger.info("Saved telemetry safely in local cache queue. Will retry in 24 hours.")
            
        self.last_upload_timestamp = time.time()

    def run(self):
        """Core real-time tracking loop."""
        # Grab first frame to select ROI
        ret, first_frame = self.cap.read()
        if not ret:
            logger.error("Could not capture initial frame from camera.")
            return
            
        self.select_roi(first_frame)
        
        logger.info("Starting fringe tracking loop. Press 'q' to quit.")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                logger.warn("Frame capture failed. Retrying...")
                time.sleep(0.1)
                continue
                
            # 1. Convert to grayscale and crop to selected ROI
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            x, y, w, h = self.roi
            roi_gray = gray[y:y+h, x:x+w]
            
            # 2. Extract 1D cross-section through the center of the ring pattern
            # We average vertically across 5 rows to reduce CMOS sensor speckle noise
            center_row = h // 2
            slice_1d = np.mean(roi_gray[center_row-2 : center_row+3, :], axis=0)
            
            # 3. Apply Gaussian smoothing to eliminate high-frequency noise
            smoothed_profile = cv2.GaussianBlur(slice_1d.reshape(1, -1), (1, 15), 0).flatten()
            
            # 4. Find sub-pixel peaks
            peaks = self.find_subpixel_peaks(smoothed_profile)
            
            if not peaks:
                # Laser is misaligned or beam blocked
                if not self.headless:
                    cv2.putText(frame, "LASER MISALIGNED / BLOCKED", (20, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.imshow("Agora@Home - People's Interferometer", frame)
                continue
                
            # Initialize baseline peaks on the first valid frame
            if self.baseline_peaks is None:
                self.baseline_peaks = peaks
                logger.info(f"Baseline initialized with {len(peaks)} interference peaks: {peaks}")
                continue
                
            # 5. Calculate phase shift relative to baseline
            # We align and find the mean distance shift of current peaks compared to closest baseline peaks
            shifts = []
            for peak in peaks:
                closest_baseline = min(self.baseline_peaks, key=lambda b: abs(b - peak))
                # Max distance threshold to prevent ring index mismatches
                if abs(closest_baseline - peak) < 25.0:
                    shifts.append(peak - closest_baseline)
                    
            if shifts:
                current_shift = float(np.mean(shifts))
                self.hourly_shifts.append(current_shift)
            else:
                current_shift = 0.0
                
            # 6. Local 1-Hour Binning & Logging
            if time.time() - self.last_hour_timestamp >= 3600.0:
                self.log_hourly_data()
                
            # 7. Daily 24-Hour Cloud Upload
            if self.upload and (time.time() - self.last_upload_timestamp >= 86400.0):
                self.trigger_upload()
                
            # 8. GUI Visualization (Only if not running headless)
            if not self.headless:
                # Draw the tracked ROI box
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Draw tracked peak coordinates onto the frame
                for peak in peaks:
                    cv2.circle(frame, (x + int(peak), y + center_row), 3, (0, 0, 255), -1)
                    
                # Overlay real-time stats
                cv2.putText(frame, f"Tracked Peaks: {len(peaks)}", (20, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                cv2.putText(frame, f"Fringe Shift: {current_shift:+.4f} px", (20, 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
                cv2.putText(frame, f"Hourly Samples: {len(self.hourly_shifts)}", (20, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
                cv2.putText(frame, "Controls: [q]=Quit | [r]=Reset Baseline | [s]=Select ROI", (20, h + y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                            
                cv2.imshow("Agora@Home - People's Interferometer", frame)
                
                # Handle keyboard inputs
                key = cv2.waitKey(30) & 0xFF
                if key == ord('q'):
                    logger.info("Quitting fringe tracking application.")
                    break
                elif key == ord('r'):
                    self.baseline_peaks = peaks
                    logger.info(f"Baseline reset. New reference: {self.baseline_peaks}")
                elif key == ord('s'):
                    self.select_roi(frame)
            else:
                # Headless console logging every 10 seconds to save CPU cycles
                if len(self.hourly_shifts) % 100 == 0:
                    logger.info(f"Fringe shift: {current_shift:+.4f} px | Samples: {len(self.hourly_shifts)}")
                time.sleep(0.1)
                
        # Cleanup
        self.cap.release()
        if not self.headless:
            cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agora@Home: Chameleon Dark Sector Interferometer Fringe Tracker")
    parser.add_argument("--device", type=int, default=0, help="Camera device index (default: 0)")
    parser.add_argument("--width", type=int, default=640, help="Camera frame width (default: 640)")
    parser.add_argument("--height", type=int, default=480, help="Camera frame height (default: 480)")
    parser.add_argument("--headless", action="store_true", help="Run in console-only headless mode (for Raspberry Pi server)")
    parser.add_argument("--upload", action="store_true", help="Enable 24-hour binned phase upload to central server")
    parser.add_argument("--server", type=str, default=None, help="Custom FastAPI server URL")
    
    args = parser.parse_args()
    
    tracker = FringeTracker(
        device=args.device,
        resolution=(args.width, args.height),
        headless=args.headless,
        upload=args.upload,
        server_url=args.server
    )
    
    try:
        tracker.run()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user. Shutting down gracefully.")
        tracker.log_hourly_data() # Save any remaining binned data before exiting
