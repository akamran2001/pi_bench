
class Main {
    public static double calc_pi(int n) {
        double pi_4 = 1.0;
        double denom = 3.0;
        double op = -1.0;
        for (int i = 0; i < n; i++) {
            pi_4 += op * (1.0 / denom);
            op *= -1.0;
            denom += 2.0;
        }
        return pi_4 * 4.0;
    }

    public static void main(String[] args) {
        int n = 1000;
        try {
            n = Integer.parseInt(args[0]);
        } catch (Exception e) {
            System.out.println(e);
        }
        long startTime = System.nanoTime();
        double pi = calc_pi(n);
        long endTime = System.nanoTime();
        double timeElapsed = (endTime - startTime) * 1e-9;
        System.out.printf("Pi using %d additions is %f and took %f seconds in Java", n, pi, timeElapsed);
    }
}