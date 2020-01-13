package cs;

import java.awt.Color;
import java.awt.geom.Point2D.Double;
import java.io.File;
import java.io.IOException;
import java.lang.invoke.MethodHandles;

public class Image_03 extends CSDP {
	static final int IMAGE_WIDTH_IN = 5;
	static final int IMAGE_HEIGHT_IN = 5;
	static final int DPI = 300;

	static final int NUM_THREADS = 64;
	static final int NUM_SAMPLES = 10000000;
	static final int kA = 2;
	static final int kB = 3;
	
	static final Color BACKGROUND = Color.WHITE;
	static final Color FOREGROUND = Color.BLUE;
	
	public Image_03() {
		super(BACKGROUND, FOREGROUND);
	}

	class CircleCalculator extends PointCalculator {

		@Override
		public Double calculate(double k, double theta, double cx, double cy, int imageSize) {
			double radius = imageSize / 2 * .99;
			return circle(k * theta, radius, cx, cy);
		}

	}

	public static void main(String[] args) throws IOException {
		if (args.length != 1) {
			throw new IllegalArgumentException(args.length + " arguments");
		}
		File outputDir = new File(args[0]);
		if (!outputDir.isDirectory()) {
			throw new IllegalArgumentException(outputDir + " not a directory");
		}
		System.out.println(args[0]);
		String className = MethodHandles.lookup().lookupClass().getSimpleName();
		className = className.toLowerCase();
		File imageName = new File(outputDir, className + ".png");

		int width = IMAGE_WIDTH_IN * DPI;
		int height = IMAGE_HEIGHT_IN * DPI;

		Image_03 imageCDSP = new Image_03();
		PointCalculator calculator = imageCDSP.new CircleCalculator();
		imageCDSP.makeImage(height, width, imageName, NUM_THREADS, NUM_SAMPLES, kA, kB, calculator);
	}
}
