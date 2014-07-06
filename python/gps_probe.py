#!/usr/bin/env python
from gnuradio import gr
import pprint;
import pmt
import time;

class gps_probe(gr.sync_block):
    def __init__(self, parent, target):
        gr.sync_block.__init__(self, 
                name = "pdu_timestamp",
                in_sig = [],
                out_sig = []);
        self.parent = parent
        self.target = target
        self.message_port_register_in(pmt.intern("pdus"));
        self.message_port_register_out(pmt.intern("pdus"));
        self.set_msg_handler(pmt.intern("pdus"), self.handler);  

    def work(self, input_items, output_items):
        assert(False)

    def handler(self, pdu):
        uhd_source = eval("self.parent.%s"%(self.target));
#        print dir(uhd_source)
        # grab all mboard sensor data
        mbs = uhd_source.get_mboard_sensor_names();
        d = {};  
        for k in mbs:
            v = uhd_source.get_mboard_sensor(k);
            d[k] = v.value
        d["gain"] = uhd_source.get_gain();
        #pprint.pprint(d);
        meta = pmt.to_pmt(d);
        self.message_port_pub(pmt.intern("pdus"), pmt.cons(meta, pmt.PMT_NIL));

