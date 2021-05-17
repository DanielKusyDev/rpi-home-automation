# Protocol specification for communication with the controller

# Rpard

The protocol message consists of rows delimeted by EOL `\r\n`. Each row has two values separated with `:` sign.
First value is a name of the attribute, and the second is an actual value. Right we have only two types as we
expect only numbers to be sent over the protocol.TY

###Request

| Field | Value | Type      |                 |
|-------|-------|-----------|-----------------|
| SNSR  | 1     | int       |                 |
| TYP   | DGT   | str       | DGT, ANL        |
| VAL   | 5     | int, float| (0, 1)          |

### Response
| Field | Value | Type |     |
|-------|-------|------|-----|
| CODE  | 1     | int  | 0,1 |
| DESC  | Error | str  |     |