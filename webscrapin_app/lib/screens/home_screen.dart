import 'package:flutter/material.dart';
import 'package:webscrapin_app/services/api_service.dart';
import 'package:webscrapin_app/screens/result_screen.dart';
import 'package:webscrapin_app/widgets/url_input.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _urlController = TextEditingController();
  bool _isLoading = false;

  Future<void> _scrapeWebsite() async {
    if (_urlController.text.isEmpty) return;

    setState(() => _isLoading = true);
    
    try {
      final data = await ApiService.scrapeWebsite(_urlController.text);
      if (!mounted) return;
      
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ResultsScreen(data: data),
        ),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Web Scraper')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            UrlInput(controller: _urlController),
            const SizedBox(height: 20),
            _isLoading
                ? const CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: _scrapeWebsite,
                    child: const Text('Analizar Sitio'),
                  ),
          ],
        ),
      ),
    );
  }
}