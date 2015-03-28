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
        (ometa, data) = (pmt.to_python(pmt.car(pdu)), pmt.cdr(pdu))   

        d = {};  
        try:
            # grab all mboard sensor data
            uhd_source = eval("self.parent.%s"%(self.target));
            mbs = uhd_source.get_mboard_sensor_names();
            for k in mbs:
                v = uhd_source.get_mboard_sensor(k);
                d[k] = v.value
            d["gain"] = uhd_source.get_gain();
            d["gps_present"] = True
        except AttributeError:
            d["gps_present"] = False
        
        #pprint.pprint(d);
        ometa.update( d );
        self.message_port_pub(pmt.intern("pdus"), pmt.cons(pmt.to_pmt(ometa), data));

