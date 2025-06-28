import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Web Security Analyzer',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const WebAnalyzerScreen(),
    );
  }
}

class WebAnalyzerScreen extends StatefulWidget {
  const WebAnalyzerScreen({super.key});

  @override
  _WebAnalyzerScreenState createState() => _WebAnalyzerScreenState();
}

class _WebAnalyzerScreenState extends State<WebAnalyzerScreen> {
  final TextEditingController _urlController = TextEditingController();
  bool _isLoading = false;
  Map<String, dynamic>? _analysisResult;

  Future<void> _analyzeWebsite() async {
    if (_urlController.text.isEmpty) return;

    setState(() {
      _isLoading = true;
      _analysisResult = null;
    });

    try {
      final response = await http.post(
        Uri.parse('http://10.100.80.119:5000/api/scrape'), // Reemplaza con tu IP
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'url': _urlController.text}),
      );

      if (response.statusCode == 200) {
        setState(() {
          _analysisResult = json.decode(response.body);
        });
      } else {
        throw Exception('Error al analizar el sitio');
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    } finally {
      setState(() => _isLoading = false);
    }
  }

  Widget _buildSecurityIndicator(Map<String, dynamic> security) {
    final score = security['puntuacion'] ?? 0;
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Análisis de Seguridad', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            LinearProgressIndicator(
              value: score / 100,
              backgroundColor: Colors.grey[200],
              color: score > 70 ? Colors.green : score > 40 ? Colors.amber : Colors.red,
            ),
            const SizedBox(height: 10),
            Text('Puntuación: $score/100', style: TextStyle(
              color: score > 70 ? Colors.green : score > 40 ? Colors.amber : Colors.red,
              fontWeight: FontWeight.bold
            )),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                Chip(
                  label: Text('SSL: ${security['ssl'] ? '✅' : '❌'}'),
                  backgroundColor: security['ssl'] ? Colors.green[100] : Colors.red[100],
                ),
                Chip(
                  label: Text('Cookies: ${security['cookies'] ? '⚠️' : '✅'}'),
                  backgroundColor: security['cookies'] ? Colors.orange[100] : Colors.green[100],
                ),
                Chip(
                  label: Text('Formularios: ${security['formularios'] ? '⚠️' : '✅'}'),
                  backgroundColor: security['formularios'] ? Colors.orange[100] : Colors.green[100],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildContentSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Contenido Extraído', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 10),
        if (_analysisResult?['headings'] != null && _analysisResult!['headings'].isNotEmpty)
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Encabezados:', style: TextStyle(fontWeight: FontWeight.bold)),
              ..._analysisResult!['headings'].map<Widget>((h) => Text('• $h')).toList(),
              const SizedBox(height: 15),
            ],
          ),
        if (_analysisResult?['links'] != null && _analysisResult!['links'].isNotEmpty)
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Enlaces encontrados:', style: TextStyle(fontWeight: FontWeight.bold)),
              ..._analysisResult!['links'].take(5).map<Widget>((link) => Text('• $link')).toList(),
            ],
          ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Analizador Web'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _urlController,
              decoration: const InputDecoration(
                labelText: 'Ingresa URL',
                hintText: 'https://ejemplo.com',
                border: OutlineInputBorder(),
                prefixIcon: Icon(Icons.link),
              ),
              keyboardType: TextInputType.url,
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _isLoading ? null : _analyzeWebsite,
              child: _isLoading 
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text('Analizar Sitio'),
            ),
            const SizedBox(height: 30),
            if (_isLoading)
              const CircularProgressIndicator()
            else if (_analysisResult != null)
              Expanded(
                child: SingleChildScrollView(
                  child: Column(
                    children: [
                      _buildSecurityIndicator(_analysisResult!['security']),
                      const SizedBox(height: 20),
                      _buildContentSection(),
                    ],
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}