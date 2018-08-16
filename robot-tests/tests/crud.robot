*** Settings ***
Library       Collections
Resource      ../global_vars.robot


Library       libs.Cleaner    WITH NAME    Cleaner
Library       libs.ControllerClient    ${CONTROLLER_ENDPOINT}    WITH NAME    Controller


Test Setup    Log To Console    Using Controller endpoint ${CONTROLLER_ENDPOINT}


Force Tags     crud_suite    sdn_workshop


*** Keywords ***


Sample Keyword
    [Arguments]    ${i can have arguments}
    Log To Console    so this keyword is basically a function
    [Return]    with a return value

Perform Teardown
    [Arguments]    ${network_name}
    Controller.Clean Data
    Cleaner.Remove Network    ${network_name}

*** Variables ***


${CONTROLLER_ENDPOINT}    ${CONTROLLER_IP}:${CONTROLLER_PORT}


*** Test Cases ***


Docker Positive Validation 1
    [Tags]    docker_validation_1
    [Documentation]    Tests docker container creation

    ${myagent}    Set Variable    Ala
    Controller.Create Agent    ${myagent}
    Controller.Assert Container Exists    ${myagent}


Docker Positive Validation 2
    [Tags]    docker_validation_2
    [Documentation]    Tests docker container deletion

    ${myagent}    Set Variable    Ola
    Run Keyword And Expect Error    *    Controller.Assert Container Exists    ${myagent}
    Controller.Create Agent    ${myagent}
    Controller.Assert Container Exists    ${myagent}

    Controller.Remove Agent    ${myagent}
    Run Keyword And Expect Error    *    Controller.Assert Container Exists    ${myagent}


Network Positive Validation
    [Tags]   net_validation_1
    [Documentation]  Tests network positive validation

    ${mynetwork}    Set Variable    Network-1
    Controller.Create Network    ${mynetwork}    192.168.0.0/24

    [Teardown]    Perform Teardown    ${mynetwork}


Network Negative Validation Wrong CIDR 1
    [Tags]   net_validation_2
    [Documentation]  Tests network negative validation wrong mask

    Run Keyword And Expect Error    *    Controller.Create Network    Network-1    192.168.0.0/80

    [Teardown]    Perform Teardown    Network-1


Network Negative Validation Wrong CIDR 2
    [Tags]   net_validation_3
    [Documentation]  Tests network negative validation wrong ip subnet

    Run Keyword And Expect Error    *    Controller.Create Network    Network-1    192.168.0.0.1/12

    [Teardown]    Perform Teardown    Network-1


Network Negative Validation Wrong CIDR 3
    [Tags]   net_validation_4
    [Documentation]  Tests network negative validation empty cidr

    Run Keyword And Expect Error    *    Controller.Create Network    Network-1    ${NONE}

    [Teardown]    Perform Teardown    Network-1


Network Negative Validation Wrong CIDR 4
    [Tags]   net_validation_5    exclude_todo
    [Documentation]  Tests network negative validation empty name

    Run Keyword And Expect Error    *    Controller.Create Network    ${NONE}    192.168.0.0/24

    [Teardown]    Perform Teardown    ${NONE}


Logical Port Positive Validation
    [Tags]    lp_validation_1
    [Documentation]    Tests logical port positive validation

    ${mynetwork}    Set Variable    Network-11
    ${myagent}    Set Variable    Ala-1
    Controller.Create Agent    ${myagent}
    Controller.Create Network    ${mynetwork}    192.168.0.0/24
    Controller.Create Logical Port    ${mynetwork}    ${myagent}

    [Teardown]    Perform Teardown    ${mynetwork}


Logical Port Negative Validation No Network
    [Tags]    lp_validation_2
    [Documentation]    Tests logical port negative validation no network

    ${myagent}    Set Variable    Ala-1
    Controller.Create Agent    ${myagent}
    Run Keyword And Expect Error    *    Controller.Create Logical Port    Network-2    ${myagent}
    [Teardown]    Controller.Clean Data