import 'package:flutter/material.dart';

class SecurityIndicator extends StatelessWidget {
  final Map<String, dynamic> securityData;

  const SecurityIndicator({super.key, required this.securityData});

  @override
  Widget build(BuildContext context) {
    final score = securityData['puntuacion'] ?? 0;
    Color getColor(int score) {
      if (score >= 70) return Colors.green;
      if (score >= 40) return Colors.orange;
      return Colors.red;
    }

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Seguridad del Sitio', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            LinearProgressIndicator(
              value: score / 100,
              backgroundColor: Colors.grey[200],
              color: getColor(score),
            ),
            const SizedBox(height: 10),
            Text('Puntuación: $score/100'),
            const SizedBox(height: 10),
            Wrap(
              spacing: 10,
              children: [
                Chip(
                  label: Text('SSL: ${securityData['ssl'] ? '✅' : '❌'}'),
                  backgroundColor: securityData['ssl'] ? Colors.green[100] : Colors.red[100],
                ),
                Chip(
                  label: Text('Cookies: ${securityData['cookies'] ? '⚠️' : '✅'}'),
                  backgroundColor: securityData['cookies'] ? Colors.orange[100] : Colors.green[100],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}