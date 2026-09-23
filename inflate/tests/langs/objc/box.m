#import <Foundation/Foundation.h>

@interface Box : NSObject
@end

@implementation Box

- (int)helper:(int)value {
    return value + 1;
}

- (int)greet:(int)value {
    return [self helper:value] * 2;
}

- (int)runner {
    return [self greet:3];
}

@end
