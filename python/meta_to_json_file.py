#!/usr/bin/env python
from gnuradio import gr
import json,time,os,pmt

class meta_to_json_file(gr.sync_block):
    def __init__(self, filename="/tmp/gr.msg.store.json.out"):
        gr.sync_block.__init__(self, 
                name = "meta_to_json_file",
                in_sig = [],
                out_sig = []);
        self.message_port_register_in(pmt.intern("pdus"));
        self.set_msg_handler(pmt.intern("pdus"), self.handler);  
        subs = {"hostname":os.uname()[1], "time":time.time()}
        self.fn = filename % subs;
        self.f = open(self.fn, "w");
        print "WARNING: Writing JSON object trace to %s"%(self.fn);

    def work(self, input_items, output_items):
        assert(False)

    def handler(self, pdu):
        meta = pmt.to_python(pmt.car(pdu))
        metaj = json.dumps(meta, sort_keys=True, indent=4,  separators=(',', ': '));
        self.f.write(metaj);
        self.f.write("\n");
        self.f.flush();
