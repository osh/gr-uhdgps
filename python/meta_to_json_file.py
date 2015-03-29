#!/usr/bin/env python
#
#  Copyright 2015 Tim O'Shea
# 
#  This file is part of gr-uhdgps.
#  
#  gr-uhdgps is free software: you can redistribute it and/or modify it under the terms of the
#  GNU General Public License as published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#  
#  gr-uhdgps is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  
#  See the GNU General Public License for more details. You should have received a copy of the GNU
#  General Public License along with gr-uhdgps. If not, see <http://www.gnu.org/licenses/>.
#  
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
