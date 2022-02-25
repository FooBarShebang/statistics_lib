# Entire Library Requirements and Tests Traceability List

## Relation between modules, classes and the requirements and tests indexing

* global requirements - 00x
* module **base_functions** - 10x
* module **ordered_functions** - 2xy
* module **data_classes** - 3xy

## Requirements vs Tests Traceability

| **Requirement ID** | **Covered in test(s)** | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------- | :----------------------- |
| REQ-FUN-000        | TEST-A-000             | NO                       |
| REQ-FUN-001        | TEST-A-000             | NO                       |
| REQ-SIO-000        | TEST-A-001             | NO                       |
| REQ-SIO-001        | TEST-A-001             | NO                       |
| REQ-INT-000        | TEST-I-000             | NO                       |
| REQ-AWM-000        | TEST-D-000             | NO                       |
| REQ-USE-000        | TEST-D-001             | NO                       |
| REQ-IAR-000        | TEST-D-002             | NO                       |
| REQ-IAR-001        | TEST-D-003             | NO                       |
| REQ-IAR-002        | TEST-D-002             | NO                       |
| REQ-UDR-000        | TEST-I-001             | NO                       |
| REQ-FUN-100        | TEST-A-100             | YES                      |
| REQ-FUN-101        | TEST-T-100             | YES                      |
| REQ-AWM-100        | TEST-T-101             | YES                      |
| REQ-AWM-101        | TEST-T-102             | YES                      |
| REQ-FUN-200        | TEST-A-200             | YES                      |
| REQ-FUN-201        | TEST-T-200             | YES                      |
| REQ-FUN-210        | TEST-T-210             | YES                      |
| REQ-FUN-220        | TEST-T-220             | YES                      |
| REQ-FUN-230        | TEST-T-230             | YES                      |
| REQ-FUN-240        | TEST-T-240             | YES                      |
| REQ-FUN-250        | TEST-T-250             | YES                      |
| REQ-FUN-260        | TEST-T-260             | YES                      |
| REQ-FUN-270        | TEST-T-270             | YES                      |
| REQ-FUN-280        | TEST-T-280             | YES                      |
| REQ-FUN-290        | TEST-T-290             | YES                      |
| REQ-FUN-2A0        | TEST-T-2A0             | YES                      |
| REQ-AWM-200        | TEST-T-201             | YES                      |
| REQ-AWM-201        | TEST-T-202             | YES                      |
| REQ-FUN-300        | TEST-A-300             | NO                       |
| REQ-FUN-310        | TEST-T-316             | NO                       |
| REQ-FUN-311        | TEST-T-316             | NO                       |
| REQ-FUN-312        | TEST-T-317             | NO                       |
| REQ-FUN-313        | TEST-T-317             | NO                       |
| REQ-FUN-320        | TEST-T-323             | NO                       |
| REQ-FUN-321        | TEST-T-323             | NO                       |
| REQ-FUN-322        | TEST-T-324             | NO                       |
| REQ-AWM-300        | TEST-T-310, TEST-T-320 | NO                       |
| REQ-AWM-301        | TEST-T-311, TEST-T-321 | NO                       |
| REQ-AWM-302        | TEST-T-312, TEST-T-322 | NO                       |
| REQ-AWM-310        | TEST-T-313             | NO                       |
| REQ-AWM-311        | TEST-T-314             | NO                       |
| REQ-AWM-312        | TEST-T-315             | NO                       |

| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| NO                                           | Under development             |
