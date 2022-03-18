# Entire Library Requirements and Tests Traceability List

## Relation between modules, classes and the requirements and tests indexing

* global requirements - 00x
* module **base_functions** - 10x
* module **ordered_functions** - 2xy
* module **data_classes** - 3xy
* module **distribution_classes** - 40x
* module **special_functions** - 5xy

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
| REQ-FUN-300        | TEST-A-300             | YES                      |
| REQ-FUN-310        | TEST-T-316             | YES                      |
| REQ-FUN-311        | TEST-T-316             | YES                      |
| REQ-FUN-312        | TEST-T-317             | YES                      |
| REQ-FUN-313        | TEST-T-317             | YES                      |
| REQ-FUN-314        | TEST-T-318             | YES                      |
| REQ-FUN-315        | TEST-D-300             | YES                      |
| REQ-FUN-320        | TEST-T-323             | YES                      |
| REQ-FUN-321        | TEST-T-323             | YES                      |
| REQ-FUN-322        | TEST-T-324             | YES                      |
| REQ-FUN-323        | TEST-T-325             | YES                      |
| REQ-FUN-324        | TEST-D-300             | YES                      |
| REQ-AWM-300        | TEST-T-310, TEST-T-320 | YES                      |
| REQ-AWM-301        | TEST-T-311, TEST-T-321 | YES                      |
| REQ-AWM-302        | TEST-T-312, TEST-T-322 | YES                      |
| REQ-AWM-310        | TEST-T-313             | YES                      |
| REQ-AWM-311        | TEST-T-314             | YES                      |
| REQ-AWM-312        | TEST-T-315             | YES                      |
| REQ-FUN-500        | TEST-A-500             | NO                       |
| REQ-FUN-510        | TEST-T-510             | YES                      |
| REQ-FUN-520        | TEST-T-520             | YES                      |
| REQ-FUN-530        | TEST-T-530             | NO                       |
| REQ-FUN-540        | TEST-T-540             | YES                      |
| REQ-FUN-550        | TEST-T-550             | NO                       |
| REQ-FUN-560        | TEST-T-560             | NO                       |
| REQ-AWM-500        | TEST-T-500             | NO                       |
| REQ-AWM-501        | TEST-T-501             | NO                       |


| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| NO                                           | Under development             |
