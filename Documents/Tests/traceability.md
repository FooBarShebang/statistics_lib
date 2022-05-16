# Entire Library Requirements and Tests Traceability List

## Relation between modules, classes and the requirements and tests indexing

* global requirements - 00x
* module **base_functions** - 10x
* module **ordered_functions** - 2xy
* module **data_classes** - 3xy
* module **distribution_classes** - 40x
* module **special_functions** - 5xy
* module **inverse_distributions** - 60x
* module **stat_test** - 7xy

## Requirements vs Tests Traceability

| **Requirement ID** | **Covered in test(s)** | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------- | :----------------------- |
| REQ-FUN-000        | TEST-A-000             | YES                      |
| REQ-FUN-001        | TEST-A-000             | YES                      |
| REQ-SIO-000        | TEST-A-001             | YES                      |
| REQ-SIO-001        | TEST-A-001             | YES                      |
| REQ-INT-000        | TEST-I-000             | YES                      |
| REQ-AWM-000        | TEST-D-000             | YES                      |
| REQ-USE-000        | TEST-D-001             | YES                      |
| REQ-IAR-000        | TEST-D-002             | YES                      |
| REQ-IAR-001        | TEST-D-003             | YES                      |
| REQ-IAR-002        | TEST-D-002             | YES                      |
| REQ-UDR-000        | TEST-I-001             | YES                      |
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
| REQ-FUN-400        | TEST-A-400             | YES                      |
| REQ-FUN-401        | TEST-T-400, TEST-T-401 | YES                      |
| REQ-FUN-402        | TEST-T-402             | YES                      |
| REQ-FUN-403        | TEST-T-403             | YES                      |
| REQ-FUN-404        | TEST-T-404             | YES                      |
| REQ-FUN-405        | TEST-T-405             | YES                      |
| REQ-FUN-406        | TEST-T-406             | YES                      |
| REQ-FUN-407        | TEST-D-400             | YES                      |
| REQ-FUN-408        | TEST-D-400             | YES                      |
| REQ-AWM-400        | TEST-T-407             | YES                      |
| REQ-AWM-401        | TEST-T-408             | YES                      |
| REQ-FUN-500        | TEST-A-500             | YES                      |
| REQ-FUN-510        | TEST-T-510             | YES                      |
| REQ-FUN-520        | TEST-T-520             | YES                      |
| REQ-FUN-530        | TEST-T-530             | YES                      |
| REQ-FUN-540        | TEST-T-540             | YES                      |
| REQ-FUN-550        | TEST-T-550             | YES                      |
| REQ-FUN-560        | TEST-T-560             | YES                      |
| REQ-AWM-500        | TEST-T-500             | YES                      |
| REQ-AWM-501        | TEST-T-501             | YES                      |
| REQ-FUN-600        | TEST-A-600             | YES                      |
| REQ-FUN-601        | TEST-T-600, TEST-T-601 | YES                      |
| REQ-FUN-602        | TEST-T-602             | YES                      |
| REQ-FUN-603        | TEST-T-603             | YES                      |
| REQ-FUN-604        | TEST-T-604             | YES                      |
| REQ-FUN-605        | TEST-T-605             | YES                      |
| REQ-FUN-606        | TEST-T-606             | YES                      |
| REQ-FUN-607        | TEST-D-600             | YES                      |
| REQ-FUN-608        | TEST-D-600             | YES                      |
| REQ-AWM-600        | TEST-T-607             | YES                      |
| REQ-AWM-601        | TEST-T-608             | YES                      |
| REQ-FUN-700        | TEST-A-700             | YES                      |
| REQ-FUN-710        | TEST-T-710             | YES                      |
| REQ-FUN-720        | TEST-T-720             | YES                      |
| REQ-FUN-730        | TEST-T-730             | YES                      |
| REQ-FUN-740        | TEST-T-740             | YES                      |
| REQ-FUN-750        | TEST-T-750             | YES                      |
| REQ-FUN-760        | TEST-T-760             | YES                      |
| REQ-FUN-770        | TEST-T-770             | YES                      |
| REQ-FUN-780        | TEST-T-780             | YES                      |
| REQ-FUN-790        | TEST-T-790             | YES                      |
| REQ-FUN-7A0        | TEST-T-7A0             | YES                      |
| REQ-FUN-7B0        | TEST-T-7B0, TEST-D-700 | YES                      |
| REQ-FUN-7B1        | TEST-T-7B0, TEST-D-700 | YES                      |
| REQ-SIO-700        | TEST-T-702             | YES                      |
| REQ-SIO-701        | TEST-T-702             | YES                      |
| REQ-SIO-702        | TEST-T-702             | YES                      |
| REQ-AWM-700        | TEST-T-700             | YES                      |
| REQ-AWM-701        | TEST-T-701             | YES                      |

| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| YES                                          | All tests are passed          |
