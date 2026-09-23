use strict;
use warnings;

package Box {
    sub helper {
        my ($value) = @_;
        return $value + 1;
    }

    sub greet {
        my ($value) = @_;
        return helper($value) * 2;
    }

    sub runner {
        return greet(3);
    }
}

1;
