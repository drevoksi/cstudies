using System.Text.RegularExpressions;

string number = "7182";

// \A   match at the start of the string
// \z   match at the end of the string
// \d   match a decimal digit
// *    match zero or more of the previous character
// []   match one of the characters in the brackets
Regex isEven = new (@"\A\d*[0, 2, 4, 6, 8]\z");

Console.WriteLine(isEven.IsMatch(number));