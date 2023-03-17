
### Dynamic Out-of-Order (OoO) scheduling
- Dynamic Out-of-Order (OoO) scheduling : technique used in modern processors to improve performance by executing instructions in an order different from their program order
- This allows the processor to take **advantage of available resources** and **execute instructions that are not dependent on each other in parallel**. 
- **Conservative Load-Store Ordering** is a memory ordering technique used to ensure correct memory access in OoO processors.
- In a restricted set of simplified instructions, **dynamic OoO scheduling with conservative load-store ordering** can be implemented by analyzing the dependencies between instructions and ensuring that **instructions are executed in the correct order**. The simplified instruction set may limit the available resources and dependencies between instructions, making it easier to implement this technique.
- When implementing conservative load-store ordering, the processor ensures that all memory **operations are executed in the order they appear in the program**. This helps to prevent memory hazards that can lead to incorrect program behavior. For example, if an instruction writes to a memory location that is later read by another instruction, the processor must ensure that the write operation completes before the read operation is executed.
- Overall, dynamic OoO scheduling with conservative load-store ordering on a restricted set of simplified instructions can improve performance by allowing the processor to execute instructions in parallel while maintaining correct program behavior.

- 2 inst per cycle
- in stall we dont WB

### Instruction Type : 
- R (Operation)
- IMMEDIATE
- LOAD
- STALL


### Stages in pipeline :
- FETCH (simple) 
- DECODE
- RENAME
- DISPATCH
- ISSUE
- WRITE_BACK
- COMMIT (simple)
