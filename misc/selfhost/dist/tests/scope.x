f() { v = 1; }

v;

g(v) { v = 2; }
h() { v = v + 1; }

main() {
	v = 4;
	f(); g(3); h();
	write([v + 48]);
}
