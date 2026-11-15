# Intelligent Work Allocation and Labor Fairness Protocol

## 1. Principles of Fair Task Distribution
In community enterprises, work allocation must balance two competing priorities:
1. **Order Timeliness:** Ensuring the entire bulk order is finished on or before the contract delivery date.
2. **Equity and Member Well-being:** Preventing work hoarding by well-connected members while avoiding overburdening members who have caregiving responsibilities.

## 2. Hard Capacity Constraints
- A member's maximum feasible daily production capacity is strictly bounded:
  $$\text{Feasible Daily Quantity} \le \text{Available Hours Per Day} \times 1.5\text{ units/hour}$$
- Under no circumstances will the system recommend assigning a quantity that would require more working hours than the member has formally committed.
- Any existing active backlog from uncompleted prior tasks is subtracted from the member's available capacity before assigning new work.

## 3. Skill Alignment
- Members tagged with specialized skills (e.g., "zari embroidery", "pattern cutting", "leather craft") receive priority assignment for high-complexity order components.
- Standard assembly and finishing tasks are rotated among apprentices to promote skill development.

## 4. Measuring Allocation Equity
- The system computes **Jain's Fairness Index** across all member allocations:
  $$J(x_1, \dots, x_n) = \frac{(\sum_{i=1}^n x_i)^2}{n \sum_{i=1}^n x_i^2}$$
- An index score between 0.85 and 1.0 indicates a balanced, highly equitable allocation across the group.

