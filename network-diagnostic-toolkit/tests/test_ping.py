from netdiag.ping import parse_ping_output

def test_parse_windows_ping():
    text='''Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),\nMinimum = 2ms, Maximum = 7ms, Average = 4ms'''
    loss, mn, avg, mx = parse_ping_output(text)
    assert (loss,mn,avg,mx)==(0.0,2.0,4.0,7.0)

def test_parse_linux_ping():
    text='''4 packets transmitted, 4 received, 0% packet loss, time 3004ms\nrtt min/avg/max/mdev = 1.100/2.200/3.300/0.100 ms'''
    loss,mn,avg,mx=parse_ping_output(text)
    assert loss==0 and mn==1.1 and avg==2.2 and mx==3.3

def test_parse_loss_only():
    loss,*rest=parse_ping_output('4 packets transmitted, 2 received, 50% packet loss')
    assert loss==50 and rest==[None,None,None]
