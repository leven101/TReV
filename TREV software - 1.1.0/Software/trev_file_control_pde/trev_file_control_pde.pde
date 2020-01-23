void setup() {
  String[] lines = loadStrings("/Users/abby/test.txt");
  println(lines[0]);
  text(lines[0], 10, 100);
}
