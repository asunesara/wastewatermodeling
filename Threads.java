import java.net.Socket;
import java.util.Random;
import java.io.*;
import java.net.*;

/*Instructions:
 * -initialize 2 20x20 matrices with random values
 * -create 5 threads
 * -each thread computes 1/5 of product matrix
 * -main thread should wait for all threads to complete and print result
 * -call join after all computations are done to get final result
 */
class Matrix {

    public static int[][] multiplyMatrices(int[][] m1, int[][] m2, int size, int row)
    {
        int[][] answer = new int[size][size];
        for (int i = 0; i < 2; i++) {
            for (int col = 0; col < m1[0].length; col++) {
                answer[row + i][col] = dotProduct(m1, m2, col, i);
                //System.out.print(answer[row + i][col] + " ");
            }
            System.out.println();
        }
        System.out.println();
        return answer;
    }

    public static int dotProduct(int[][] c1, int[][] c2, int col, int row) {
        int product = 0;
        for (int i = 0; i < c2.length; i++) {
            product += (c1[row][i] * c2[i][col]);
        }
        return product;
    }

    public static void main(String args[]) {

        Random ran = new Random();
        int size = 10; //length and width of matrices
        int[][] m1 = new int[size][size];
        int[][] m2 = new int[size][size];

        //initialize matrices with random values between 0 and 20
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                m1[i][j] = ran.nextInt(20);
                m2[i][j] = ran.nextInt(20);
            }
        }

        //print first matrix
        System.out.println("Matrix 1: ");
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                System.out.print(m1[i][j] + " ");
            }
            System.out.println();
        }

        //print second matrix
        System.out.println("\nMatrix 2: ");
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                System.out.print(m2[i][j] + " ");
            }
            System.out.println();
        }
        
        System.out.print("\nProduct Matrix");
        for (int x = 0; x < 5; x++) {
            final int count = x; //measures current row
            Thread t = new Thread(new Runnable() {
                public void run() {
                    int[][] m1Part = new int[size/5][size]; //first matrix rows are split into 1/5 original size
                    int[][] finalMatrix = new int[size][size];
                    for (int i = 0; i < size/5; i++) {
                        for (int j = 0; j < size; j++) {
                            m1Part[i][j] = m1[i + count][j];
                            //System.out.println(m1Part[i][j]);
                        }
                    }
                    
                    finalMatrix = multiplyMatrices(m1Part, m2, size, count);
                    for (int i = 0; i < size; i++) {
                        for (int j = 0; i < 4; i++) {
                            System.out.print(finalMatrix[count + j][i] + " ");
                        }
                    }
                }
            } );
            t.start(); 
            try {t.join();} catch(InterruptedException e) {};
        }
    }
}
