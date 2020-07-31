#pragma once
#include <Arduino.h>

byte charToByte(const char& by) {
  switch (by) {
    case '0': return 0; break;
    case '1': return 1; break;
    case '2': return 2; break;
    case '3': return 3; break;
    case '4': return 4; break;
    case '5': return 5; break;
    case '6': return 6; break;
    case '7': return 7; break;
    case '8': return 8; break;
    case '9': return 9; break;
    case 'A': return 0xa; break;
    case 'B': return 0xb; break;
    case 'C': return 0xc; break;
    case 'D': return 0xd; break;
    case 'E': return 0xe; break;
    case 'F': return 0xf; break;
    case 'a': return 0xa; break;
    case 'b': return 0xb; break;
    case 'c': return 0xc; break;
    case 'd': return 0xd; break;
    case 'e': return 0xe; break;
    case 'f': return 0xf; break;
  }
}

void fromString(const String& str, byte* ref) {
  *ref = charToByte(str[0]) << 4 | charToByte(str[1]);
}
