import 'package:flutter/material.dart';

class UrlInput extends StatelessWidget {
  final TextEditingController controller;

  const UrlInput({super.key, required this.controller});

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      decoration: InputDecoration(
        labelText: 'URL del sitio web',
        hintText: 'https://ejemplo.com',
        border: const OutlineInputBorder(),
        prefixIcon: const Icon(Icons.link),
        suffixIcon: IconButton(
          icon: const Icon(Icons.clear),
          onPressed: () => controller.clear(),
        ),
      ),
      keyboardType: TextInputType.url,
    );
  }
}