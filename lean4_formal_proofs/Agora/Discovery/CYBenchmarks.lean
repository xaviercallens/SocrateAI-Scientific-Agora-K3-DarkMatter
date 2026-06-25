import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Tactic

namespace Agora.Discovery.CYBenchmarks

/-- The Apéry sequence: A(n) = Σ_{k=0}^{n} C(n,k)² · C(n+k,k)² -/
def Apery (n : ℕ) : ℤ :=
  ↑((Finset.range (n + 1)).sum (fun k => (Nat.choose n k)^2 * (Nat.choose (n + k) k)^2))

/-- The Domb sequence: D(n) = Σ_{k=0}^{n} C(n,k)² · C(2k,k) · C(2(n-k), n-k) -/
def Domb (n : ℕ) : ℤ :=
  ↑((Finset.range (n + 1)).sum (fun k => (Nat.choose n k)^2 * (Nat.choose (2*k) k) * (Nat.choose (2*(n-k)) (n-k))))

/-- The Franel-5 sequence: F_5(n) = Σ_{k=0}^{n} C(n,k)⁵ -/
def Franel5 (n : ℕ) : ℤ :=
  ↑((Finset.range (n + 1)).sum (fun k => (Nat.choose n k)^5))

/-- The Almkvist-Zudilin sequence: Z(n) = Σ_{k=0}^{⌊n/3⌋} (-1)ᵏ 3ⁿ⁻³ᵏ (3k)!/(k!)³ C(n,3k) C(n+k,k) -/
def AZ (n : ℕ) : ℤ :=
  (Finset.range (n / 3 + 1)).sum (fun k =>
    (-1 : ℤ)^k * (3 : ℤ)^(n - 3*k) * ↑(Nat.choose (3*k) k * Nat.choose (2*k) k * Nat.choose n (3*k) * Nat.choose (n + k) k)
  )

/-- Apéry boundary supercongruence mod 5³ -/
theorem apery_supercongruence_5 : Apery 5 % 125 = 5 := by decide

/-- Domb boundary supercongruence mod 5³ -/
theorem domb_supercongruence_5 : Domb 5 % 125 = 4 := by decide

/-- Franel-5 boundary supercongruence mod 5³ -/
theorem franel5_supercongruence_5 : Franel5 5 % 125 = 2 := by decide

/-- Almkvist-Zudilin boundary supercongruence mod 5³ -/
theorem az_supercongruence_5 : AZ 5 % 125 = 3 := by decide

end Agora.Discovery.CYBenchmarks
