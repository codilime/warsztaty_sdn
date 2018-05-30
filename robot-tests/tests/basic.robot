*** Settings ***
Library       Collections
Resource      ../global_vars.robot

Library       libs.Cleaner    WITH NAME    Cleaner
Library       libs.ConnectivityChecker    WITH NAME     Checker
Library       libs.ControllerAdapter    ${CONTROLLER_ENDPOINT}    WITH NAME    Controller

Test Setup    Log To Console    Using Controller endpoint ${CONTROLLER_ENDPOINT}

Force Tags     basic_suite    sdn_workshop

*** Variables ***
${CONTROLLER_ENDPOINT}    ${CONTROLLER_IP}:${CONTROLLER_PORT}

*** Keywords ***
Perform Teardown
    [Arguments]    ${network_name}
    Controller.Clean Data
    Cleaner.Remove Network    ${network_name}

*** Test Cases ***
Simplest VPN
    [Tags]   simple_vpn_1
    [Documentation]  Tests simple vpn 1-network-1-lp
    ${mynetwork}    Set Variable    Network-111
    Controller.Create Network    ${mynetwork}    192.168.0.0/24
    Controller.Create Logical Port    ${mynetwork}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}

    # Sanity check
    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    127.0.0.1
    Run Keyword If    ${result} == ${False}   Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${False}    Fail

    [Teardown]    Perform Teardown    ${mynetwork}



Basic VPN
    [Tags]   simple_vpn_2
    [Documentation]  Tests simple vpn 1-network-2-lp
    ${mynetwork}    Set Variable    Network-112
    Controller.Create Network    ${mynetwork}    192.168.0.0/24
    Controller.Create Logical Port    ${mynetwork}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}
    Controller.Create Logical Port    ${mynetwork}    ${AGENT_OLA_ID}    ${AGENT_OLA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.11
    Run Keyword If    ${result} == ${False}    Fail

    [Teardown]    Perform Teardown    ${mynetwork}



Threeway VPN
    [Tags]   simple_vpn_3    exclude_todo
    [Documentation]  Tests simple vpn 1-network-3-lp
    ${mynetwork}    Set Variable    Network-113
    Controller.Create Network    ${mynetwork}    192.168.0.0/24
    Controller.Create Logical Port    ${mynetwork}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}
    Controller.Create Logical Port    ${mynetwork}    ${AGENT_OLA_ID}    ${AGENT_OLA_IP}
    Controller.Create Logical Port    ${mynetwork}    ${AGENT_KASIA_ID}    ${AGENT_KASIA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.11
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_KASIA_IP}:${AGENT_KASIA_PORT}    192.168.0.18
    Run Keyword If    ${result} == ${False}    Fail

    [Teardown]    Perform Teardown    ${mynetwork}



Standard VPN With Two Networks
    [Tags]   simple_vpn_4
    [Documentation]  Tests simple vpn 2-network-3-lp
    ${mynetwork_1}    Set Variable    Network-200
    ${mynetwork_2}    Set Variable    Network-300

    Controller.Create Network    ${mynetwork_1}    192.168.0.0/24
    Controller.Create Network    ${mynetwork_2}    192.168.100.0/24

    Controller.Create Logical Port    ${mynetwork_1}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}
    Controller.Create Logical Port    ${mynetwork_1}    ${AGENT_OLA_ID}    ${AGENT_OLA_IP}
    Controller.Create Logical Port    ${mynetwork_2}    ${AGENT_KASIA_ID}    ${AGENT_KASIA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.11
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_KASIA_IP}:${AGENT_KASIA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${True}    Fail

    ${result}    Checker.Ping    ${AGENT_KASIA_IP}:${AGENT_KASIA_PORT}    192.168.0.11
    Run Keyword If    ${result} == ${True}    Fail

    [Teardown]    Run Keywords    Controller.Clean Data
    ...           AND    Cleaner.Remove Network    ${mynetwork_1}
    ...           AND    Cleaner.Remove Network    ${mynetwork_2}



Standard VPN With Two Networks
    [Tags]   simple_vpn_5
    Cleaner.Remove Network    Network-200
    Cleaner.Remove Network    Network-200
    Cleaner.Remove Network    Network-300


Simple Logic Port Removal
    [Tags]   simple_lp_removal_1
    ${mynetwork}    Set Variable    Network-123
    Controller.Create Network    ${mynetwork}    192.168.0.0/24
    Controller.Create Logical Port    ${mynetwork}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}
    Controller.Create Logical Port    ${mynetwork}    ${AGENT_OLA_ID}    ${AGENT_OLA_IP}


#    This was tested already in "Basic VPN", so I think it shouldn't be duplicated here
#    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
#    Run Keyword If    ${result} == ${False}    Fail
#
#    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.11
#    Run Keyword If    ${result} == ${False}    Fail


    Controller.Remove Logical Port    ${mynetwork}    ${AGENT_ALA_ID}


    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${True}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.11
    Run Keyword If    ${result} == ${True}    Fail

    [Teardown]    Perform Teardown    ${mynetwork}



Standard Logic Port Change With Two Networks
    [Tags]   simple_lp_removal
    [Documentation]  2-network-3-lp
    ${mynetwork_1}    Set Variable    Network-200
    ${mynetwork_2}    Set Variable    Network-300

    Controller.Create Network    ${mynetwork_1}    192.168.0.0/24
    Controller.Create Network    ${mynetwork_2}    192.168.100.0/24

    Controller.Create Logical Port    ${mynetwork_1}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}
    Controller.Create Logical Port    ${mynetwork_1}    ${AGENT_OLA_ID}    ${AGENT_OLA_IP}
    Controller.Create Logical Port    ${mynetwork_2}    ${AGENT_KASIA_ID}    ${AGENT_KASIA_IP}


#    This was tested already in "Standard VPN With Two Networks"
#    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
#    Run Keyword If    ${result} == ${False}    Fail
#
#    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.11
#    Run Keyword If    ${result} == ${False}    Fail
#
#    ${result}    Checker.Ping    ${AGENT_KASIA_IP}:${AGENT_KASIA_PORT}    192.168.0.2
#    Run Keyword If    ${result} == ${True}    Fail
#
#    ${result}    Checker.Ping    ${AGENT_KASIA_IP}:${AGENT_KASIA_PORT}    192.168.0.11
#    Run Keyword If    ${result} == ${True}    Fail


    Controller.Remove Logical Port    ${mynetwork_1}    ${AGENT_ALA_ID}
    Controller.Create Logical Port    ${mynetwork_2}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}


    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${True}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.11
    Run Keyword If    ${result} == ${True}    Fail

    ${result}    Checker.Ping    ${AGENT_KASIA_IP}:${AGENT_KASIA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${True}    Fail

    ${result}    Checker.Ping    ${AGENT_KASIA_IP}:${AGENT_KASIA_PORT}    192.168.0.11
    Run Keyword If    ${result} == ${True}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.100.2
    Run Keyword If    ${result} == ${False}    Fail


    [Teardown]    Run Keywords    Controller.Clean Data
    ...           AND    Cleaner.Remove Network    ${mynetwork_1}
    ...           AND    Cleaner.Remove Network    ${mynetwork_2}






Simple One Container In Two Networks
    [Documentation]  2-network-3-lp Ola-Ala-Kasia
    ${mynetwork_1}    Set Variable    Network-200
    ${mynetwork_2}    Set Variable    Network-300

    Controller.Create Network    ${mynetwork_1}    192.168.0.0/24
    Controller.Create Network    ${mynetwork_2}    192.168.100.0/24

    Controller.Create Logical Port    ${mynetwork_1}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}
    Controller.Create Logical Port    ${mynetwork_1}    ${AGENT_OLA_ID}    ${AGENT_OLA_IP}

    Controller.Create Logical Port    ${mynetwork_2}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}
    Controller.Create Logical Port    ${mynetwork_2}    ${AGENT_KASIA_ID}    ${AGENT_KASIA_IP}

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.0.11
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.100.2
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_ALA_IP}:${AGENT_ALA_PORT}    192.168.100.11
    Run Keyword If    ${result} == ${False}    Fail

    ${result}    Checker.Ping    ${AGENT_KASIA_IP}:${AGENT_KASIA_PORT}    192.168.0.2
    Run Keyword If    ${result} == ${True}    Fail

    ${result}    Checker.Ping    ${AGENT_KASIA_IP}:${AGENT_KASIA_PORT}    192.168.0.11
    Run Keyword If    ${result} == ${True}    Fail

    [Teardown]    Run Keywords    Controller.Clean Data
    ...           AND    Cleaner.Remove Network    ${mynetwork_1}
    ...           AND    Cleaner.Remove Network    ${mynetwork_2}
