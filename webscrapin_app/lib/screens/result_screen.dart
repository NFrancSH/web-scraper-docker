import 'package:flutter/material.dart';
import 'package:webscrapin_app/widgets/security_indicator.dart';

class ResultsScreen extends StatelessWidget {
  final Map<String, dynamic> data;

  const ResultsScreen({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(data['url'] ?? 'Resultados')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (data['security'] != null)
              SecurityIndicator(securityData: data['security']),
            
            const SizedBox(height: 20),
            const Text('Encabezados:', style: TextStyle(fontWeight: FontWeight.bold)),
            ..._buildList(data['headings']),
            
            const SizedBox(height: 20),
            const Text('Enlaces:', style: TextStyle(fontWeight: FontWeight.bold)),
            ..._buildList(data['links']),
            
            const SizedBox(height: 20),
            const Text('Imágenes:', style: TextStyle(fontWeight: FontWeight.bold)),
            ..._buildList(data['images']),
          ],
        ),
      ),
    );
  }

  List<Widget> _buildList(List<dynamic>? items) {
    if (items == null || items.isEmpty) {
      return [const Text('No se encontraron elementos')];
    }
    
    return items.map((item) => ListTile(
      title: Text(item.toString()),
      dense: true,
    )).toList();
  }
}