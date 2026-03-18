module design_cmp_lt_2_52976f7a7318b84b(a0, a1, b0, b1, y);
  input a0, a1, b0, b1;
  output y;
  assign y = (1 & ~a1 & b1) | (~(a1 ^ b1) & ~a0 & b0);
endmodule
