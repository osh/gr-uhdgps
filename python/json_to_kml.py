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
from lxml import etree
import kmldom, kmlengine, kmlbase, sys, datetime, numpy, json
from operator import itemgetter
from optparse import OptionParser

# reformat angles
def gpsconv(s):
    [ms,d] = s.split(".");
    [m,s] = [ms[0:len(ms)-2], ms[-2:]];
    f = float(m) + float(s)/60.0 + (float(d)/10000.0)/60.0;
    return f;

def convert_json_to_kml(f_in, f_out):
    
    # load JSON file
    fc = open(f_in,"r").read();
    fc = fc.split("}")[:-1];
    rec = map(lambda x: json.loads(x + "}"), fc);

    # parse GPS data strings into lat/lon/el
    for r in rec:
        fix = r["gps_gpgga"].split(",");
        r["lat"] = gpsconv(fix[2]) * (+1) # N
        r["lon"] = gpsconv(fix[4]) * (-1) # W
        r["elev"] = float(fix[9])
    
    # sort in time order
    rec = sorted(rec, key=itemgetter('gps_time')) 

    # set up KML file
    factory = kmldom.KmlFactory.GetFactory() 
    root = factory.CreateKml() 
    document = factory.CreateDocument() 
    document.set_name("GR-UHDGPS RSSI Measurement: Track Data") 

    # prepare to re-scale RSSI range to plotting elevations...
    rssis = map(lambda x: x["power"], rec)
    rssi_range = (min(rssis), max(rssis))
    plot_el_range = (0,50.0)

    # set up plots 
    el_key = ["power"];
    el_scale = [(plot_el_range[1] - plot_el_range[0]) / (rssis[1] - rssis[0])]
    el_off = [plot_el_range[0] - rssi_range[0] ]
    labels = ["RSSI"];

    # loop through generating them
    for i in range(0,len(el_key)):
        (k, s, n, o) = (el_key[i], el_scale[i], labels[i], el_off[i])
        # add our track
        factory = kmldom.KmlFactory_GetFactory()
        placemark = factory.CreatePlacemark()
        placemark.set_name(n)
        coordinates = factory.CreateCoordinates()
        for i in range(0,len(rec)):
            x = rec[i];
            coordinates.add_latlngalt(x["lat"], x["lon"], 0)
            coordinates.add_latlngalt(x["lat"], x["lon"], ((x[k])+o)*s)
            coordinates.add_latlngalt(x["lat"], x["lon"], 0)
        linestring = factory.CreateLineString()
        linestring.set_tessellate(True);
        linestring.set_coordinates(coordinates)
        linestring.set_altitudemode(1)
        placemark.set_geometry(linestring)
        document.add_feature(placemark);

    # write the kml file
    root.set_feature(document) 
    kml_file = kmlengine.KmlFile.CreateFromImport(root) 
    f = open(f_out,"w");
    f.write( kml_file.SerializeToString()[1]  );
    f.close();


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="in_file",
                  help="Input File", metavar="FILE")
    parser.add_option("-o", "--output",
                  dest="out_file", help="Output File")
    (options, args) = parser.parse_args()
    if(options.in_file == None or options.out_file == None):
        parser.print_help()
        sys.exit(-1)

    convert_json_to_kml(options.in_file, options.out_file)
    print "Done"



