module design_half_adder_1_72b94c35fd30860f(a, b, sum, cout);
  input a, b;
  output sum, cout;
  assign sum = (a ^ b);
  assign cout = (a & b);
endmodule
