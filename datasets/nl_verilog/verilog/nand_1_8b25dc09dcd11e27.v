module design_nand_1_8b25dc09dcd11e27(a, b, y);
  input a, b;
  output y;
  assign y = ~(a & b);
endmodule
