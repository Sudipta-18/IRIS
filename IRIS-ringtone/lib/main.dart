import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:ringtone/ringtone.dart';
// import 'package:vibrate/vibrate.dart';
import 'package:cron/cron.dart';

class RingtoneExample extends StatefulWidget {
  @override
  _RingtoneExampleState createState() => _RingtoneExampleState();
}

class _RingtoneExampleState extends State<RingtoneExample> {
  @override
  void initState() {
    sec5Timer().then((value) => print("Timer running..."));
  }

  bool _isPlaying = false;
  String data = "0";

  bool isStopped = false; //global

  Future fetchFileData() async {
    String responseText;
    responseText = await rootBundle.loadString('textFile/text.txt');
    data = responseText;
    if (data == "1") {
      _isPlaying = !_isPlaying;
      Ringtone.play();
    }
  }

  Future sec5Timer() async {
    Timer.periodic(Duration(seconds: 5), (timer) {
      if (isStopped) {
        timer.cancel();
      }
      fetchFileData();
      print("in sec5timer");
    });
  }

  // crontimer()

  // if(data == "1") {
  //   Ringtone.play();
  // }

  _playRingtone() async {
    if (_isPlaying) {
      Ringtone.stop();

      setState(() {
        _isPlaying = !_isPlaying;
      });
    } else {
      Ringtone.play();

      setState(() {
        _isPlaying = !_isPlaying;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('IRIS')),
      body: Center(
          child: RaisedButton(
        child: Text(_isPlaying ? "Stop Ringtone" : "Play Ringtone"),
        color: Colors.red,
        onPressed: _playRingtone,
      )),
    );
  }
}

void main() async => runApp(new MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return new MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'IRIS',
      theme: new ThemeData(primarySwatch: Colors.red),
      home: new RingtoneExample(),
    );
  }
}
