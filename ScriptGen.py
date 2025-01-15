class Generator(object):
    def __init__(self, S_AS, P_AS, S_IP, P_IP, P_Name):
        self.S_AS = S_AS
        self.P_AS = P_AS
        self.S_IP = S_IP
        self.P_IP = P_IP
        self.P_Name = P_Name



    def bgp_get_script(self):
        return '</br>' '<b>'"Numbered VTI:"'</b>' \
            '</br>' "add vpn tunnel 10 type numbered local " + str(self.S_IP) + " remote " + str(self.P_IP) + " peer " + str(self.P_Name) + \
            '</br>' '<b>'"BGP:"'</b>' \
            '</br>' "set as " + str(self.S_AS) + \
            '</br>' "set bgp external remote-as "+ str(self.P_AS) + " on" \
            '</br>' "set bgp external remote-as "+ str(self.P_AS) +" peer "+ str(self.P_IP) +" on" \
            '</br>' "set bgp external remote-as "+ str(self.P_AS) +" peer "+ str(self.P_IP) +" as-override on" \
            '</br>' "set bgp external remote-as "+ str(self.P_AS) +" peer "+ str(self.P_IP) +" holdtime 30" \
            '</br>' "set bgp external remote-as "+ str(self.P_AS) +" peer "+ str(self.P_IP) +" keepalive 10" \
            '</br>' "set inbound-route-filter bgp-policy 514 based-on-as as "+ str(self.P_AS) +" on" \
            '</br>' "set inbound-route-filter bgp-policy 514 accept-all-ipv4" \
            '</br>' '<b>'"Route-Redistribution:"'</b>' \
            '</br>' "set route-redistribution to bgp-as "+ str(self.P_AS) +" from interface eth1 on"


    def ospf_get_script( S_IP, P_IP, P_Name):
        return '</br>' '<b>'"Numbered VTI:"'</b>' \
            '</br>' "add vpn tunnel 10 type numbered local " + str(S_IP) + " remote " + str(P_IP) + " peer " + str(P_Name) + \
            '</br>' '<b>'"OSPF:"'</b>' \
            '</br>' "set ospf area backbone on" \
            '</br>' "set ospf interface vpnt1 area backbone on" \
            '</br>' "set ospf interface eth1 area backbone on"

