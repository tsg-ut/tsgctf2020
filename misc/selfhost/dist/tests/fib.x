print_int(n) {
	if (n < 0) {
		write([45]);
		n = - n;
	}
	if (n == 0) write([48]);
	else {
		s = [];
		while (n > 0) {
			s = [48 + n % 10] + s;
			n = n / 10;
		}
		write(s);
	}
	write([10]);
}

read_int() {
	res = 0;
	sign = 1;
	c = read();
	if (c == "-") {
		sign = -1;
		c = read();
	}
	ok = 1;
	while (ok) {
		if (48 <= c && c <= 57) {
			res = res * 10 + c - 48;
			c = read();
		}
		else ok = 0;
	}
	return res * sign;
}

fib(n) {
	if (n <= 1) return 1;
	else return fib(n-1) + fib(n-2);
}

main(){
	print_int(fib(read_int()));
}
