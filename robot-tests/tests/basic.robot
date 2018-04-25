*** Settings ***
Library       Collections
Resource      ../global_vars.robot

Library       libs.ControllerAdapter    ${CONTROLLER_IP}    WITH NAME    Controller

Test Setup    Log To Console    Using Controller endpoint ${CONTROLLER_ENDPOINT}
Test Teardown

Force Tags     crud_suite

*** Keywords ***
Basic Keyword
    Log To Console    Starting test

*** Variables ***
${CONTROLLER_ENDPOINT}    ${CONTROLLER_IP}:${CONTROLLER_PORT}

*** Test Cases ***
Positive Validation
    [Tags]   validation_1
    [Documentation]  Tests positive validation
    Controller.Create Network    Network-1    192.168.0.0/24

Negative Validation Wrong CIDR 1
    [Tags]   validation_2
    [Documentation]  Tests negative validation wrong mask
    Run Keyword And Expect Error    Controller.Create Network    Network-1    192.168.0.0/80

Negative Validation Wrong CIDR 2
    [Tags]   validation_3
    [Documentation]  Tests negative validation wrong ip subnet
    Run Keyword And Expect Error    Controller.Create Network    Network-1    192.168.0.0.1/12

Negative Validation Wrong CIDR 3
    [Tags]   validation_4
    [Documentation]  Tests negative validation empty cidr
    Run Keyword And Expect Error    Controller.Create Network    Network-1    ${NONE}

Negative Validation Wrong CIDR 4
    [Tags]   validation_5
    [Documentation]  Tests negative validation empty name
    Run Keyword And Expect Error    Controller.Create Network    ${NONE}    192.168.0.0/24

