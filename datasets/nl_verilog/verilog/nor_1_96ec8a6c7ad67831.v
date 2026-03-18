module design_nor_1_96ec8a6c7ad67831(a, b, y);
  input a, b;
  output y;
  assign y = ~(a | b);
endmodule
