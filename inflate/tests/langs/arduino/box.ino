int helper(int value) {
  return value + 1;
}

int greet(int value) {
  return helper(value) * 2;
}

void runner() {
  Serial.println(greet(3));
}
