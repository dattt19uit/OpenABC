module design_encoder8_8_58c82c051ddf7a9e(d0, d1, d2, d3, d4, d5, d6, d7, y0, y1, y2);
  input d0, d1, d2, d3, d4, d5, d6, d7;
  output y0, y1, y2;
  assign y0 = d1 | d3 | d5 | d7;
  assign y1 = d2 | d3 | d6 | d7;
  assign y2 = d4 | d5 | d6 | d7;
endmodule
