module design_ripple_adder_2_9fae569888e819fb(a0, a1, b0, b1, sum0, sum1, cout);
  input a0, a1, b0, b1;
  output sum0, sum1, cout;
  assign sum0 = (a0 ^ b0 ^ 0);
  assign sum1 = (a1 ^ b1 ^ ((a0 & b0) | (a0 & 0) | (b0 & 0)));
  assign cout = ((a1 & b1) | (a1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))) | (b1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))));
endmodule
