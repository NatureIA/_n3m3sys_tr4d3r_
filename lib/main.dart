
import 'package:flutter/material.dart';

void main() => runApp(NemesisApp());

class NemesisApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Nêmesis',
      theme: ThemeData.dark(),
      home: Scaffold(
        appBar: AppBar(title: Text('NÊMESIS')),
        body: Center(child: Text('IA conectada e pronta')),
      ),
    );
  }
}
