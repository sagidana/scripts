export class Box {
    private size = 1;

    helper(value: number): number {
        return value + this.size;
    }

    greet(value: number): number {
        return this.helper(value) * 2;
    }

    runner(): number {
        return this.greet(3);
    }
}
