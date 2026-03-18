module design_ripple_adder_3_eeb81367829b02d4(a0, a1, a2, b0, b1, b2, sum0, sum1, sum2, cout);
  input a0, a1, a2, b0, b1, b2;
  output sum0, sum1, sum2, cout;
  assign sum0 = (a0 ^ b0 ^ 0);
  assign sum1 = (a1 ^ b1 ^ ((a0 & b0) | (a0 & 0) | (b0 & 0)));
  assign sum2 = (a2 ^ b2 ^ ((a1 & b1) | (a1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))) | (b1 & ((a0 & b0) | (a0 & 0) | (b0 & 0)))));
  assign cout = ((a2 & b2) | (a2 & ((a1 & b1) | (a1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))) | (b1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))))) | (b2 & ((a1 & b1) | (a1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))) | (b1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))))));
endmodule
