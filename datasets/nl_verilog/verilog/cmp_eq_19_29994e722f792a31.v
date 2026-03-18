module design_cmp_eq_19_29994e722f792a31(a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, b18, y);
  input a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, b18;
  output y;
  assign y = ~(a0 ^ b0) & ~(a1 ^ b1) & ~(a2 ^ b2) & ~(a3 ^ b3) & ~(a4 ^ b4) & ~(a5 ^ b5) & ~(a6 ^ b6) & ~(a7 ^ b7) & ~(a8 ^ b8) & ~(a9 ^ b9) & ~(a10 ^ b10) & ~(a11 ^ b11) & ~(a12 ^ b12) & ~(a13 ^ b13) & ~(a14 ^ b14) & ~(a15 ^ b15) & ~(a16 ^ b16) & ~(a17 ^ b17) & ~(a18 ^ b18);
endmodule
