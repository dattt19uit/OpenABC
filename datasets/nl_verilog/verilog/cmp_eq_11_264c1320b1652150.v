module design_cmp_eq_11_264c1320b1652150(a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, y);
  input a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10;
  output y;
  assign y = ~(a0 ^ b0) & ~(a1 ^ b1) & ~(a2 ^ b2) & ~(a3 ^ b3) & ~(a4 ^ b4) & ~(a5 ^ b5) & ~(a6 ^ b6) & ~(a7 ^ b7) & ~(a8 ^ b8) & ~(a9 ^ b9) & ~(a10 ^ b10);
endmodule
