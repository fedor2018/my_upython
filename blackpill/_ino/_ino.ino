/* 
 * The Secrets of an Inexpensive, Ubiquitous Chinese LCD Display
 * Example 1: Writing text to the display
 *
 * Portions (c) 2018 Marcio Teixeira
 * Portions (c) 2018 Aleph Objects, Inc.
 * 
 * The code in this page is free software: you can
 * redistribute it and/or modify it under the terms of the GNU
 * General Public License (GNU GPL) as published by the Free Software
 * Foundation, either version 3 of the License, or (at your option)
 * any later version.  The code is distributed WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU GPL for more details.
 * 
 */

#define LCD_SID  PB15 //5
#define LCD_SCLK PB13 //4

void lcd_send(bool value) {
  digitalWrite(LCD_SID, value);
  digitalWrite(LCD_SCLK, HIGH);
  digitalWrite(LCD_SCLK, LOW);
}

void lcd_sync(bool rs, bool rw) {
  lcd_send(1); // Sync 1
  lcd_send(1); // Sync 2
  lcd_send(1); // Sync 3
  lcd_send(1); // Sync 4
  lcd_send(1); // Sync 5
  lcd_send(rw);
  lcd_send(rs);
  lcd_send(0);
}

void lcd_data(uint8_t data) {
  lcd_send(data & 0b10000000);
  lcd_send(data & 0b01000000);
  lcd_send(data & 0b00100000);
  lcd_send(data & 0b00010000);
  lcd_send(0);
  lcd_send(0);
  lcd_send(0);
  lcd_send(0);
  lcd_send(data & 0b00001000);
  lcd_send(data & 0b00000100);
  lcd_send(data & 0b00000010);
  lcd_send(data & 0b00000001);
  lcd_send(0);
  lcd_send(0);
  lcd_send(0);
  lcd_send(0);
}

void lcd_cmd(uint8_t cmd) {
  lcd_sync(0, 0); // All commands have rs=0 and rw=0
  lcd_data(cmd);
  delayMicroseconds(72); // The datasheet specifies that commands take 72u to execute
}

void lcd_extended_function_set(bool extended, bool graphics) {
  lcd_cmd(  0b00100000 | 
    (extended   ? 0b00000100 : 0) |
    (graphics   ? 0b00000010 : 0)
  );
}

void lcd_display_status(bool display_on, bool cursor_on, bool blink_on) {
  lcd_cmd(0b00001000 |
    (display_on ? 0b0100 : 0) |
    (cursor_on  ? 0b0010 : 0) |
    (blink_on   ? 0b0001 : 0)
  );
}

void lcd_entry_mode(bool increase, bool shift) {
  lcd_cmd(        0b00000100 | 
    (increase   ? 0b00000010 : 0) |
    (shift      ? 0b00000001 : 0)
  );
}

void lcd_clear() {
  lcd_cmd(0b00000001);
  delayMicroseconds(1600); // The datasheet specifies that CLEAR requires 1.6ms
}

void lcd_set_ddram_address(uint8_t addr) {
  lcd_cmd(0b10000000 | (addr & 0b00111111));
}

void lcd_write_begin() {
  lcd_sync(1,0);
}

void lcd_write_byte(uint8_t w) {
  lcd_data(w);
}

void lcd_write_str(const char *str) {
  char c = pgm_read_byte_near(str++);
  while(c) {
     lcd_write_byte(c);
     c = pgm_read_byte_near(str++);
  }
}

void setup() {
  // Set all the pins as output
  pinMode(LCD_SID,  OUTPUT);
  pinMode(LCD_SCLK, OUTPUT);

  // Initialize the display
  lcd_extended_function_set(false, false); // Do this twice since only one bit
  lcd_extended_function_set(false, false); // can be set at a time.
  lcd_display_status(true, false, false);
  lcd_clear();
  
  // Set the address to the top of the display
  // and write some text
  lcd_set_ddram_address(0x00);
  lcd_write_begin();
  lcd_write_str(PSTR("The quick brown fox jumps over the lazy dogs. 0123456789.:,;(*!?"));
}

void loop() {
}
