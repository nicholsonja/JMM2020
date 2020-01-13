package cs;

import java.awt.Color;
import java.awt.geom.Point2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import javax.imageio.ImageIO;

import cs.CSDP.ComputeData;

/**
 * Curve Stitching Density Plot
 * 
 * @author John
 *
 */
public abstract class CSDP {
	private int[] imageData;
	private Color backgroundColor;
	private Color foregroundColor;
	protected Random rand;

	public CSDP(Color backgroundColor, Color forgroundColor) {
		rand = new Random();
		this.backgroundColor = backgroundColor;
		this.foregroundColor = forgroundColor;
	}

	synchronized void saveData(int[] remoteData) {
		for (int i = 0; i < remoteData.length; i++) {
			imageData[i] += remoteData[i];
		}
	}

	public int[] initializeData(int imageWidth, int imageHeight) {
		int[] data = new int[imageHeight * imageWidth];
		return data;
	}

	public Point2D.Double rotate(double x, double y, double angle) {
		return new Point2D.Double(x * Math.cos(angle) - y * Math.sin(angle), x * Math.sin(angle) + y * Math.cos(angle));
	}

	public Point2D.Double lemniscate(double theta, double radius) {
		return lemniscate(theta, radius, 0, 0);
	}

	public Point2D.Double lemniscate(double theta, double radius, double cx, double cy) {
		double c = Math.cos(theta);
		double s = Math.sin(theta);
		double x = (radius * c) / (1 + s * s);
		double y = (radius * s * c) / (1 + s * s);
		return new Point2D.Double(x + cx, y + cy);

	}

	public Point2D.Double circle(double theta, double radius) {
		return circle(theta, radius, 0, 0);
	}

	public Point2D.Double circle(double theta, double radius, double cx, double cy) {
		double x = Math.cos(theta) * radius + cx;
		double y = Math.sin(theta) * radius + cy;
		return new Point2D.Double(x, y);
	}

	void saveImage(int[] data, File imageName, int imageWidth, int imageHeight) throws IOException {

		int maxCount = Arrays.stream(data).max().getAsInt();

		BufferedImage bi = new BufferedImage(imageWidth, imageHeight, BufferedImage.TYPE_INT_RGB);

		double alpha;
		Color color;
		for (int y = 0; y < imageHeight; y++) {
			for (int x = 0; x < imageWidth; x++) {

				int cnt = data[y * imageWidth + x];
				if (cnt == 0) {
					alpha = 0;
				} else {
					alpha = Math.log(cnt) / Math.log(maxCount);
				}

				Color rgb = new Color(
						(int) (alpha * foregroundColor.getRed() + (1 - alpha) * backgroundColor.getRed() + .5),
						(int) (alpha * foregroundColor.getGreen() + (1 - alpha) * backgroundColor.getGreen() + .5),
						(int) (alpha * foregroundColor.getBlue() + (1 - alpha) * backgroundColor.getBlue() + .5));
				bi.setRGB(x, y, rgb.getRGB());
			}
		}
		ImageIO.write(bi, "png", imageName);
	}

	void makeImage(int height, int width, File imageName, int numThreads, int numSamples, double kA, double kB,
			PointCalculator calculator) throws IOException {
		int imageWidth = Math.min(width, height);
		int imageHeight = Math.max(width, height);

		int[] data = runDataCalculations(imageWidth, imageHeight, numThreads, numSamples, kA, kB, calculator);

		saveImage(data, imageName, imageWidth, imageHeight);

	}

	class ComputeData extends Thread {
		int imageWidth;
		int imageHeight;
		int workerId;
		int numSamples;
		double kA;
		double kB;
		PointCalculator calculator;

		public ComputeData(int workerId, int imageWidth, int imageHeight, int numSamples, double kA, double kB,
				PointCalculator calculator) {
			this.workerId = workerId;
			this.imageHeight = imageHeight;
			this.imageWidth = imageWidth;
			this.numSamples = numSamples;
			this.kA = kA;
			this.kB = kB;
			this.calculator = calculator;
		}

		@Override
		public void run() {
			int[] data = initializeData(imageWidth, imageHeight);
			int size = Math.min(imageWidth, imageHeight);

			double cx = imageWidth / 2.0;
			double cy = imageHeight / 2.0;
			double radius = imageWidth / 2.0 * .99;

			for (int n = 0; n < numSamples; n++) {
				double theta = rand.nextDouble() * 2 * Math.PI;

				Point2D.Double A = calculator.calculate(kA, theta, cx, cy, size);
				Point2D.Double B = calculator.calculate(kB, theta, cx, cy, size);
				if (A.equals(B)) {
					continue;
				}

				Point2D.Double C = calculator.getRandomPoint(A, B, cx, cy);

				int i = (int) (C.x + .5);
				int j = (int) (C.y + .5);

				data[j * imageWidth + i] += 1;
			}
			System.out.println("Finished process " + workerId);

			saveData(data);

		}
	}

	public int[] runDataCalculations(int imageWidth, int imageHeight, int numThreads, int numSamples, double kA,
			double kB, PointCalculator calculator) {
		imageData = initializeData(imageWidth, imageHeight);

		int cores = Runtime.getRuntime().availableProcessors();
		ExecutorService executor = Executors.newFixedThreadPool(cores);
		System.out.println("Cores: " + cores);

		for (int i = 0; i < numThreads; i++) {
			Runnable worker = new ComputeData(i, imageWidth, imageHeight, numSamples, kA, kB, calculator);
			executor.execute(worker);
		}
		executor.shutdown();
		try {
			executor.awaitTermination(1, TimeUnit.HOURS);
		} catch (InterruptedException e) {
			System.out.println("Termination failed");
			e.printStackTrace();
		}
		System.out.println("Finished all threads");

		return imageData;

	}

	public Point2D.Double randomPointOnPath(ArrayList<Point2D.Double> pathPoints) {
		if (pathPoints.size() < 2) {
			throw new IllegalArgumentException("Need at least two points in path");
		}

		double pathLength = 0;
		Point2D.Double currPoint = pathPoints.get(0);
		for (int pI = 1; pI < pathPoints.size(); pI++) {
			Point2D.Double point = pathPoints.get(pI);
			pathLength += Math.sqrt(Math.pow(currPoint.x - point.x, 2) + Math.pow(currPoint.y - point.y, 2));
			currPoint = point;
		}

		double r = rand.nextDouble();
		double targetDist = r * pathLength;

		double dist = 0;
		currPoint = pathPoints.get(0);

		for (int pI = 1; pI < pathPoints.size(); pI++) {
			Point2D.Double point = pathPoints.get(pI);
			double segmentLen = Math.sqrt(Math.pow(currPoint.x - point.x, 2) + Math.pow(currPoint.y - point.y, 2));

			if (dist + segmentLen >= targetDist) {
				double pointDist = (targetDist - dist) / segmentLen;
				Point2D.Double A = currPoint;
				Point2D.Double B = point;
				Point2D.Double C = new Point2D.Double((1 - pointDist) * A.x + pointDist * B.x,
						(1 - pointDist) * A.y + pointDist * B.y);
				return C;
			}
			dist += segmentLen;
			currPoint = point;
		}

		return null;

	}

	abstract class PointCalculator {

		abstract public Point2D.Double calculate(double k, double theta, double cx, double cy, int size);

		public Point2D.Double getRandomPoint(Point2D.Double a, Point2D.Double b, double cx, double cy) {

			double r = rand.nextDouble();
			double x = (1 - r) * a.x + r * b.x;
			double y = (1 - r) * a.y + r * b.y;
			return new Point2D.Double(x, y);
		}

		public Point2D.Double getRandomPoint(Point2D.Double a, Point2D.Double b, double cx, double cy,
				ArrayList<Point2D.Double> unitSegment) {
			double dist = Math.sqrt(Math.pow(a.x - b.x, 2) + Math.pow(a.y - b.y, 2));
			double theta = Math.atan2(b.y - a.y, b.x - a.x);
			ArrayList<Point2D.Double> segment = new ArrayList<Point2D.Double>();
			double c = Math.cos(theta);
			double s = Math.sin(theta);
			for (Point2D.Double p : unitSegment) {
				double x = p.x * c - p.y * s;
				double y = p.x * s + p.y * c;

				segment.add(new Point2D.Double(x * dist + a.x + cx, y * dist + a.y + cy));
			}

			return randomPointOnPath(segment);

		}
	}
}
