import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String _baseUrl = 'http://10.100.80.119:5000'; // Cambiar por tu IP

  static Future<Map<String, dynamic>> scrapeWebsite(String url) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/api/scrape'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'url': url}),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to scrape website: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }
}