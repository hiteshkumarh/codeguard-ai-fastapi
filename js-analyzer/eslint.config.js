// eslint.config.js
module.exports = [
  {
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
      globals: {
        console: "readonly",
        eval: "readonly"
      }
    },
    rules: {
      "no-eval": "error",
      "no-var": "warn"
    }
  }
];
