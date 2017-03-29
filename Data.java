public class Data {
    
    private int value;
    
    public Data() { }
    
    public void setValue(int value) {
        this.value = value;
    }
    
    public int getValue() {
        return value;
    }
    
    public boolean isSmaller(Data element) {
        return this.value < element.value ? true : false;
    }
    
    public boolean isBigger(Data element) {
        return this.value > element.value ? true : false;
    }
    
    public boolean equals(Data element) {
        return this.value == element.value ? true : false;
    }
}