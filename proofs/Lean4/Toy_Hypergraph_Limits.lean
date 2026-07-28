/-
  Toy Hypergraph Limits in Lean 4
  Formalizing edge growth and monotonic expansion under rewrite rule {x, y} -> {x, z}, {y, z}
-/

namespace ToyHypergraph

/-- Volume V(t) defined as the number of hyperedges at step t under parallel replacement -/
def hyperedge_count (t : Nat) : Nat :=
  2 ^ t

/-- Theorem: Hyperedge count strictly increases monotonically at every step -/
theorem hyperedge_count_strictly_increasing (t : Nat) :
  hyperedge_count t < hyperedge_count (t + 1) := by
  dsimp [hyperedge_count]
  have hpos : 0 < 2 ^ t := Nat.two_pow_pos t
  have hsucc : 2 ^ (t + 1) = 2 ^ t + 2 ^ t := by
    rw [Nat.pow_succ]
    exact Nat.mul_two (2 ^ t)
  rw [hsucc]
  exact Nat.lt_add_of_pos_right hpos

/-- Theorem: Delta V(t) = 2^t -/
theorem delta_volume (t : Nat) :
  hyperedge_count (t + 1) - hyperedge_count t = 2 ^ t := by
  dsimp [hyperedge_count]
  have hsucc : 2 ^ (t + 1) = 2 ^ t + 2 ^ t := by
    rw [Nat.pow_succ]
    exact Nat.mul_two (2 ^ t)
  rw [hsucc]
  exact Nat.add_sub_cancel_left (2 ^ t) (2 ^ t)

/-- Node count N(t) at step t starting from 2 initial nodes -/
def node_count (t : Nat) : Nat :=
  2 ^ t + 1

theorem node_count_strictly_increasing (t : Nat) :
  node_count t < node_count (t + 1) := by
  dsimp [node_count]
  have hpos : 0 < 2 ^ t := Nat.two_pow_pos t
  have hsucc : 2 ^ (t + 1) = 2 ^ t + 2 ^ t := by
    rw [Nat.pow_succ]
    exact Nat.mul_two (2 ^ t)
  rw [hsucc]
  omega

end ToyHypergraph
