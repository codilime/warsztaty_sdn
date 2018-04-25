*** Settings ***
Library       Collections
Resource      ../global_vars.robot

Library       libs.Cleaner
Library       libs.ControllerAdapter    ${CONTROLLER_IP}    WITH NAME    Controller

Test Setup    Log To Console    Using Controller endpoint ${CONTROLLER_ENDPOINT}
Test Teardown

Force Tags     basic_suite    sdn_workshop

#*** Keywords ***

*** Variables ***
${CONTROLLER_ENDPOINT}    ${CONTROLLER_IP}:${CONTROLLER_PORT}

*** Test Cases ***
Simplest VPN
    [Tags]   simple_vpn_1
    [Documentation]  Tests simple vpn 1-network-1-lp
    ${mynetwork}    Network-111
    Controller.Create Network    ${mynetwork}    192.168.0.0/24
    Controller.Create Logical Port    ${mynetwork}    ${AGENT_ALA_ID}    ${AGENT_ALA_IP}

    [Teardown]    Cleaner.Remove Network    ${mynetwork}

