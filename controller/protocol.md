# Protocol specification for communication with the controller

# Rpard

The protocol message consists of rows delimeted by EOL `\r\n`. Each row has two values separated with `:` sign.
First value is a name of the attribute, and the second is an actual value.

### Input message

* _SNSR_ - device specific sensor ID
* _TYP_ - either DGT for digital output or ANL for analog
* _VAL_ - actual value, integer for ANL TYP and float/integer for DGT
* _EOM_ - End Of Message. Indicates if there are more messages in a single connection

| Field | Value | Type      |                 |
|-------|-------|-----------|-----------------|
| SNSR  | RP_01 | str       |                 |
| TYP   | DGT   | str       | DGT, ANL        |
| VAL   | 5     | int, float| (0, 1)          |
| EOM   | 1     | int       | (0, 1)          |

### Response
| Field | Value | Type |     |
|-------|-------|------|-----|
| CODE  | 1     | int  | 0,1 |

#### Codes
| Code | Description            |
|------|------------------------|
| 0    | success                |
| 1    | unknown error          |
| 2    | permission error       |
| 3    | input validation error |
| 4    | not found error        |