module design_ripple_adder_4_ac815a8758948314(a0, a1, a2, a3, b0, b1, b2, b3, sum0, sum1, sum2, sum3, cout);
  input a0, a1, a2, a3, b0, b1, b2, b3;
  output sum0, sum1, sum2, sum3, cout;
  assign sum0 = (a0 ^ b0 ^ 0);
  assign sum1 = (a1 ^ b1 ^ ((a0 & b0) | (a0 & 0) | (b0 & 0)));
  assign sum2 = (a2 ^ b2 ^ ((a1 & b1) | (a1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))) | (b1 & ((a0 & b0) | (a0 & 0) | (b0 & 0)))));
  assign sum3 = (a3 ^ b3 ^ ((a2 & b2) | (a2 & ((a1 & b1) | (a1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))) | (b1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))))) | (b2 & ((a1 & b1) | (a1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))) | (b1 & ((a0 & b0) | (a0 & 0) | (b0 & 0)))))));
  assign cout = ((a3 & b3) | (a3 & ((a2 & b2) | (a2 & ((a1 & b1) | (a1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))) | (b1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))))) | (b2 & ((a1 & b1) | (a1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))) | (b1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))))))) | (b3 & ((a2 & b2) | (a2 & ((a1 & b1) | (a1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))) | (b1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))))) | (b2 & ((a1 & b1) | (a1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))) | (b1 & ((a0 & b0) | (a0 & 0) | (b0 & 0))))))));
endmodule
