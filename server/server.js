var mime = require('mime');
var formidable = require('formidable');
var http = require('http');
var fs = require('fs-extra');
var util = require('util');
var path = require('path');
var exec = require('child_process').exec;
var shortid = require('shortid');

var port = process.env.PORT || 8080;
var dataDir = "./temp/";

var streznik = http.createServer(function(zahteva, odgovor) {
   if (zahteva.url == '/') {
       posredujStaticnoVsebino(odgovor, './index.html', "");
   }
   else if(zahteva.url == '/nalozi') {
       naloziDatoteko(zahteva, odgovor);
   }
});

streznik.listen(port, function(){
    console.log("Streznik je zagnan!");
});

function posredujStaticnoVsebino(odgovor, absolutnaPotDoDatoteke, mimeType) {
        fs.exists(absolutnaPotDoDatoteke, function(datotekaObstaja) {
            if (datotekaObstaja) {
                fs.readFile(absolutnaPotDoDatoteke, function(napaka, datotekaVsebina) {
                    if (napaka) {
                        posredujNapako404(odgovor);
                    } else {
                        posredujDatoteko(odgovor, absolutnaPotDoDatoteke, datotekaVsebina, mimeType);
                    }
                })
            } else {
                posredujNapako404(odgovor);
            }
        });
}

function posredujDatoteko(odgovor, datotekaPot, datotekaVsebina, mimeType) {
    if (mimeType == "") {
        odgovor.writeHead(200, {'Content-Type': mime.lookup(path.basename(datotekaPot))});    
    } else {
        odgovor.writeHead(200, {'Content-Type': mimeType});
    }
    odgovor.end(datotekaVsebina, function() {
        if(path.dirname(datotekaPot) == './temp') {
            fs.unlink(datotekaPot);
        }
    });
}

function naloziDatoteko(zahteva, odgovor) {
    var form = new formidable.IncomingForm();
 
    form.parse(zahteva, function(napaka, polja, datoteke) {
        util.inspect({fields: polja, files: datoteke});
    });
 
    form.on('end', function(fields, files) {
        var zacasnaPot = this.openedFiles[0].path;
        var id = shortid.generate();
        var vhodnaDatoteka = dataDir + 'vhod_' + id + '.txt';
        var izhodnaDatoteka = dataDir + 'izhod_' + id + '.txt';
        fs.copy(zacasnaPot, vhodnaDatoteka, function(napaka) {  
            if (napaka) {
                posredujNapako500(odgovor);
            } else {
                var execCommand = './util/bin/sorter ' + vhodnaDatoteka + ' ' + izhodnaDatoteka;
                exec(execCommand, function(error, stdout, stderr) {
                    console.log(vhodnaDatoteka);
                    fs.unlink(vhodnaDatoteka);
                    posredujStaticnoVsebino(odgovor, izhodnaDatoteka, "");
                });
            }
        });
    });
}

function posredujNapako500(odgovor) {
    odgovor.writeHead(500, {'Content-Type': 'text/plain'});
    odgovor.write('Napaka 500: Napaka na strezniku!');
    odgovor.end();
}

function posredujNapako404(odgovor) {
    odgovor.writeHead(404, {'Content-Type': 'text/plain'});
    odgovor.write('Napaka 404: Vira ni mogoce najti!');
    odgovor.end();
}